# 新闻联播长视频、演讲稿对齐

## 原理讲解及实验代码
```python
# in theory_exp
```

## 创建视频到演讲稿的映射
```python
python create_recording2book.py
```

## 根据映射重新筛选视频和演讲稿
因为一部分数据只有视频，一部分数据只有演讲稿，我们需要筛选同时有视频和演讲稿的数据
```python
python select_data.py
```

## 创建monocut
MonoCut 对象是一个数据结构,用于表示单个音频片段及其相关信息
```python
python prepare_manifest.py
```

## 长视频分片
```python
python split_into_chunks.py
```

