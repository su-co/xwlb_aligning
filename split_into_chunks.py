#!/usr/bin/env python3
# Copyright    2023  Xiaomi Corp.        (authors: Fangjun Kuang,
#                                                  Zengwei Yao,
#                                                  Wei Kang)
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


"""
This script splits long utterances into chunks with overlaps.
Each chunk (except the first and the last) is padded with extra left side and right side.
The chunk length is: left_side + chunk_size + right_side.
"""

import logging
from pathlib import Path

from lhotse import CutSet, load_manifest_lazy



def main():
    manifest_in = Path("/media/as/ASNAS1/humiao/output/xwlb_raw_cuts_all.jsonl.gz")
    manifest_out = Path("/media/as/ASNAS1/humiao/output_split/xwlb_raw_split.jsonl")
    chunk = 30  # seconds
    extra = 2   # seconds

    if manifest_in == manifest_out:
        logging.error(
            f"Input manifest and output manifest share the same path : "
            f"{manifest_in}, the filenames should be different."
        )

    manifest_out_dir = manifest_out.parents[0]
    manifest_out_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"Processing {manifest_in}.")

    if manifest_out.is_file():
        logging.info(f"{manifest_out} already exists - skipping.")
        return

    cuts = load_manifest_lazy(manifest_in)

    cuts = cuts.cut_into_windows(
        duration=chunk, hop=chunk - extra * 2
    )
    cuts = cuts.fill_supervisions(shrink_ok=True)

    cuts.to_file(manifest_out)
    logging.info(f"Cuts saved to {manifest_out}")


if __name__ == "__main__":
    formatter = (
        "%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s"
    )
    logging.basicConfig(format=formatter, level=logging.INFO)

    main()