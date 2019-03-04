import reducer from './alternativeDrugs';
import { expect } from 'chai';
import { setAlternativeDrugs } from '../actions';

describe('alternativeDrugs reducer', () => {
  it('return the initial state', () => {
    expect(reducer(undefined, {})).to.have.lengthOf(0);
  });

  it('should handle SET_ALTERNATIVE_DRUGS', () => {
    const altDrug = {
      name: 'test'
    };

    const initialState = reducer(undefined, {});
    expect(initialState).to.deep.equal([]);

    const updatedState = reducer(initialState, {
      type: setAlternativeDrugs.type,
      payload: [altDrug]
    });

    expect(updatedState[0].name).to.equal('test');
  });
});
