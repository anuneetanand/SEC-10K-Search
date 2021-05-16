# ir_project_frontend

### Project Structure

```
├── babel.config.js
├── dist
│   ├── favicon.ico
│   └── index.html
├── package.json
├── package-lock.json
├── public
│   ├── favicon.ico
│   └── index.html
├── README.md
├── server.js
├── src
  ├── App.vue
  ├── assets
  │   ├── logo.png
  │   └── logo.svg
  ├── components
  │   ├── CompanyCard.vue
  │   ├── CompanyPage.vue
  │   ├── DocumentInfoCard.vue
  │   └── InfoTable.vue
  ├── main.js
  └── plugins
      └── vuetify.js
├── static.json
└── vue.config.js
```

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Features

#### Main Dashboard

- Has a search box (with autocomplete) of over 100+ companies. One can write down a query or simply search for a company.
- Searching for a company or a query lists down the corresponding item cards.

#### Item Cards

- Each item card contains a document, its score, date of publish as well as a small summary associated with the search query.
- Clicking on an item card opens an dropdown which elaborates the current document.

### Company Card

- It has 2 items.
- 3 balance tables.
- Clicking on the company name renders a modal with some interesting graphs about the company.
