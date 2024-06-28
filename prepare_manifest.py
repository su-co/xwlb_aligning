#!/usr/bin/env python3
# Copyright    2023  Xiaomi Corp.        (authors: Wei Kang)
#
# See ../../../../LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This file is copied and modified from
# https://github.com/lhotse-speech/lhotse/blob/master/lhotse/recipes/librilight.py

"""
About the librilight corpus

Libri-light is a benchmark for the training of automatic speech recognition (ASR)
systems with limited or no supervision.

It contains a large dataset of 60K hours of unlabelled speech from audiobooks in 
English and a small labelled dataset (10h, 1h, and 10 min) plus metrics,
trainable baseline models, and pretrained models that use these datasets.

It is covered in more detail at https://arxiv.org/abs/1912.07875.

This data is very huge - please download manually at LIBRILIGHT_URL.
"""

import logging
import json
from collections import defaultdict
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Dict

from tqdm.auto import tqdm

from lhotse.audio import Recording
from lhotse import CutSet, MonoCut
from lhotse.recipes.utils import manifests_exist
from lhotse.supervision import SupervisionSegment
from lhotse.utils import Pathlike



def _parse_utterance(
    corpus_dir: Pathlike,
    audio_path: Pathlike,
    books_dir: Pathlike,
    books_dict: Dict,
) -> MonoCut: # MonoCut 对象是一个数据结构,用于表示单个音频片段及其相关信息
    file_name = (
        str(audio_path).replace(".m4a", "").replace(str(corpus_dir) + "/", "")
    )
    speaker = str(audio_path).split("/")[-3]
    audio_path = audio_path.resolve()

    if not audio_path.is_file():
        logging.warning(f"No such file: {audio_path}")
        return None

    recording = Recording.from_file(
        path=audio_path,
        recording_id=file_name,
    )
    segment = SupervisionSegment(
        id=file_name,
        recording_id=file_name,
        start=0.0,
        duration=recording.duration,
        channel=0,
        language="Chinese",
        speaker=speaker,
    )

    return MonoCut(
        id=file_name,
        start=0.0,
        duration=recording.duration,
        channel=0,
        custom={"text_path": str(books_dir / books_dict[file_name])},
        recording=recording,
        supervisions=[segment],
    )


def _prepare_subset(
    subset: str,
    corpus_dir: Pathlike,
    books_dir: Pathlike,
    num_jobs: int = 1,
) -> CutSet:
    """
    Returns the CutSet given a dataset part.
    :param subset: str, the name of the subset.
    :param corpus_dir: Pathlike, the path of the data dir.
    :param books_dir: Path to the LibriLight books.
    :return: the CutSet
    """
    part_path = corpus_dir / subset
    audio_paths = list(part_path.rglob("*.m4a"))

    with open(books_dir / f"recording2book_{subset}.json") as f:
        books_dict = json.load(f)

    with ThreadPoolExecutor(num_jobs) as ex:
        futures = []
        cuts = []
        for audio_path in tqdm(audio_paths, desc="Distributing tasks"):
            futures.append(
                ex.submit(
                    _parse_utterance,
                    corpus_dir,
                    audio_path,
                    books_dir,
                    books_dict,
                )
            )

        for future in tqdm(futures, desc="Processing"):
            result = future.result()
            if result is None:
                continue
            cuts.append(result)
        cut_set = CutSet.from_cuts(cuts)

    return cut_set


def prepare_xwlb(
    corpus_dir: Pathlike,
    books_dir: Pathlike,
    output_dir: Pathlike,
    num_jobs: int = 1,
):
    """
    Returns the manifests which consist of the Recordings and Supervisions
    :param corpus_dir: Path to the LibriLight dataset.
    :param books_dir: Path to the LibriLight books.
    :param output_dir: Pathlike, the path where to write the manifests.
    :return: a Dict whose key is the dataset part, and the value is Dicts with the keys 'recordings' and 'supervisions'.
    """
    corpus_dir = Path(corpus_dir)
    books_dir = Path(books_dir)
    output_dir = Path(output_dir) if output_dir is not None else None

    assert corpus_dir.is_dir(), f"No such directory: {corpus_dir}"
    assert books_dir.is_dir(), f"No such directory: {books_dir}"

    logging.info("Preparing xwlb...")

    subsets = ("all",)

    if output_dir is not None:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

    for part in tqdm(subsets, desc="Dataset parts"):
        logging.info(f"Processing xwlb subset: {part}")
        if manifests_exist(
            part=part,
            output_dir=output_dir,
            prefix="xwlb",
            suffix="jsonl.gz",
        ):
            logging.info(
                f"xwlb subset: {part} already prepared - skipping."
            )
            continue

        cut_set = _prepare_subset(part, corpus_dir, books_dir, num_jobs)

        if output_dir is not None:
            cut_set.to_file(output_dir / f"xwlb_raw_cuts_{part}.jsonl.gz")


if __name__ == "__main__":
    formatter = (
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    logging.basicConfig(format=formatter, level=logging.INFO)

    corpus_dir = "/media/as/ASNAS1/humiao/xwlb_m4a"
    books_dir = "/media/as/ASNAS1/humiao/xwlbText"
    output_dir = "/media/as/ASNAS1/humiao/output"
    num_jobs = 1

    prepare_xwlb(
        corpus_dir=corpus_dir,
        books_dir=books_dir,
        output_dir=output_dir,
        num_jobs=num_jobs,
    )

    logging.info(f"Done.")