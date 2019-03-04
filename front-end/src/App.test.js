import React from 'react';
import { App } from './App';
import Enzyme from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import { expect } from 'chai';
import { shallow } from 'enzyme';
import AsyncSelect from 'react-select/lib/Async';
import ReactTable from 'react-table';
import { stub } from 'sinon';

Enzyme.configure({ adapter: new Adapter() });

it('renders without crashing', () => {
  const props = {
    alternativeDrugs: [],
    fetchAlternativeDrugs: stub(),
    setAlternativeDrugs: stub()
  };

  const wrapper = shallow(
    <App
      alternativeDrugs={props.alternativeDrugs}
      fetchAlternativeDrugs={props.fetchAlternativeDrugs}
      setAlternativeDrugs={props.setAlternativeDrugs}
    />
  );
  expect(wrapper.find('h3')).to.have.lengthOf(1);
  expect(wrapper.find(AsyncSelect)).to.have.lengthOf(1);
  expect(wrapper.find(ReactTable)).to.have.lengthOf(1);
});

it('handles selection change', () => {
  const props = {
    alternativeDrugs: [],
    fetchAlternativeDrugs: stub().returns(Promise.resolve([])),
    setAlternativeDrugs: stub()
  };

  const wrapper = shallow(
    <App
      alternativeDrugs={props.alternativeDrugs}
      fetchAlternativeDrugs={props.fetchAlternativeDrugs}
      setAlternativeDrugs={props.setAlternativeDrugs}
    />
  );
  wrapper.instance().onSelectChange();
  expect(props.setAlternativeDrugs.callCount).to.equal(1);

  wrapper.instance().onSelectChange('anything');
  expect(props.fetchAlternativeDrugs.callCount).to.equal(1);
});

it('gets default options', async () => {
  global.fetch = jest
    .fn()
    .mockImplementationOnce(() =>
      Promise.resolve({
        json() {
          return [['testing1']];
        }
      })
    )
    .mockImplementationOnce(() =>
      Promise.resolve({
        json() {
          return [['testing2']];
        }
      })
    )
    .mockImplementationOnce(() =>
      Promise.resolve({
        json() {
          return [['testing3']];
        }
      })
    );
  const props = {
    alternativeDrugs: [],
    fetchAlternativeDrugs: stub(),
    setAlternativeDrugs: stub()
  };

  const wrapper = shallow(
    <App
      alternativeDrugs={props.alternativeDrugs}
      fetchAlternativeDrugs={props.fetchAlternativeDrugs}
      setAlternativeDrugs={props.setAlternativeDrugs}
    />
  );
  let response = await wrapper.instance().searchDrugs('');
  expect(response).to.deep.equal([{ label: 'testing1', value: 'testing1' }]);
  response = await wrapper.instance().searchDrugs('valid search');
  expect(response).to.deep.equal([{ label: 'testing2', value: 'testing2' }]);
  response = await wrapper.instance().searchDrugs('va');
  expect(response).to.deep.equal([{ label: 'testing3', value: 'testing3' }]);
});
