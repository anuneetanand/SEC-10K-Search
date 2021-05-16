# ir_project_backend

### Project structure

```
├── data
│   ├── bm25_corpus1.pkl
│   ├── bm25_corpus2.pkl
│   ├── bm25.pkl
│   ├── companies
│   ├── company_index.pkl
│   ├── corpus1.json
│   ├── corpus2.json
│   ├── corpus.json
│   ├── docs.pkl
│   ├── graph_data.pkl
│   ├── index2.pkl
│   ├── index.pkl
│   ├── matrix.pkl
│   ├── new_graph_data.pkl
│   ├── runtime.txt
│   ├── summaries_items.json
│   ├── table_index.pkl
│   ├── tmp.ipynb
│   └── updated_Docs.pkl
├── helper.py
├── nltk.txt
├── Procfile
├── __pycache__
│   └── helper.cpython-36.pyc
├── README.md
├── requirements.txt
├── runtime.txt
└── server.py
```

### Project setup

#### Prerequisites

- Install the required libraries using `pip3 install -r requirements.tx`
- Download some of the heavy files in `data` folder from [here](https://drive.google.com/drive/folders/12VkxRI99jmjxtQPmWqOuLbC-bJTyxb2M).

#### Running the server
`python3 server.py`

### Project description

The server serves the request made through the dashboard by using the TF-IDF ranking scheme. 
