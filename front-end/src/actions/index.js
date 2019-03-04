import { createAction } from 'redux-starter-kit';

export const requestAlternativeDrugs = createAction(
  'REQUEST_ALTERNATIVE_DRUGS'
);
export const setAlternativeDrugs = createAction('SET_ALTERNATIVE_DRUGS');

export function fetchAlternativeDrugs(name) {
  return async function(dispatch) {
    dispatch(requestAlternativeDrugs());

    const response = await fetch(
      `api/similar_drugs?name=${name}`
    );
    const json = await response.json();
    return dispatch(setAlternativeDrugs(json));
  };
}
