import { createReducer } from 'redux-starter-kit';
import { setAlternativeDrugs } from '../actions';

const initialState = [];

const alternativeDrugs = createReducer(initialState, {
  [setAlternativeDrugs]: (state, action) => {
    return [...action.payload];
  }
});

export default alternativeDrugs;
