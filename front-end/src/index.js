import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import { configureStore } from 'redux-starter-kit';
import alternativeDrugs from './reducers/alternativeDrugs';
import { Provider } from 'react-redux';

const store = configureStore({
  reducer: {
    alternativeDrugs
  }
});

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root')
);
