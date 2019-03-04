import { fetchAlternativeDrugs } from './index';
// import { expect } from 'chai';

it('gets default options', async () => {
  global.fetch = jest.fn().mockImplementationOnce(() =>
    Promise.resolve({
      json() {
        return [];
      }
    })
  );
  const dispatch = jest.fn();
  const getState = jest.fn();
  fetchAlternativeDrugs('testing4')(dispatch, getState);
  expect(dispatch).toBeCalledWith({
    type: 'REQUEST_ALTERNATIVE_DRUGS',
    payload: undefined
  });
});
