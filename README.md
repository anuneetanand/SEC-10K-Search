# Information Retrieval on SEC 10-K Documents

The financial statements of a company provide a lot of valuable insights about it. However, extracting crucial information from these statements is time-consuming and often quite cumbersome. We propose an interactive information retrieval system that can query the financial information of a company, summarise SEC 10-K filings and visualise a company’s performance over the past few years. Our proposed system can be used by, but not limited to, investors, traders, analysts, auditors, and corporate executives.

## Folder Structure
```
.
├── Backend
│   ├── helper.py
│   ├── requirements.txt
│   └── server.py
├── Frontend
│   ├── babel.config.js
│   ├── package.json
│   ├── public
│   ├── server.js
│   ├── src
│   ├── static.json
│   └── vue.config.js
├── Other
│   ├── Notebooks
│   ├── Presentation.pdf
│   └── Report.pdf
└── README.md
```
## Setup 🛠️

### Backend
- Install the required libraries using `pip install -r requirements.txt`
- Download the data folder from [here](https://drive.google.com/drive/folders/1bidGP1Les9kusT4RcOqL_jvCKWIad3db?usp=sharing) and place it in the Backend directory

### Frontend
- Install the required node modules using ```npm install```

## Build ⚙️

### Backend
```
cd Backend
python3 server.py
```
### Frontend
```
cd Frontend
npm run serve
```

## Features :star:
- User can give natural language queries to search for relevant financial documents.
- Important parts of 10-K documents of a company are summarised.
- Important tables are extracted and presented to the user.
- Change in crucial financial indicators of a company are visualised using plots.
- Sentiment Analysis on Management's Decisions.

## Evaluation 📊
| Method      | Precision@3 | Precision@5 | Precision@10 |
| ----------- | ----------- | ----------- | ------------ |
| TF-IDF      | 0.78        | 0.74        | 0.54         |
| log(TF)-IDF | 0.48        | 0.46        | 0.41         |
| BM-25       | 0.66        | 0.65        | 0.51         |

## Team

[Anuneet Anand](https://github.com/anuneetanand)    
[Isha Gupta](https://github.com/IshaGupta18)  
[Osheen Sachdev](https://github.com/oshhh)  
[Paras Mehan](https://github.com/parasmehan123)   
[Uday Narayan Goel](https://github.com/uday2000)    
