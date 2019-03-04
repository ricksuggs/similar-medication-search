import React from 'react';
import PropTypes from 'prop-types';
import AsyncSelect from 'react-select/lib/Async';
import ReactTable from 'react-table';
import 'react-table/react-table.css';
import { ReactTableDefaults } from 'react-table';
import { connect } from 'react-redux';
import { fetchAlternativeDrugs, setAlternativeDrugs } from './actions';
import debounce from 'debounce-async';
import './App.css';

export class App extends React.Component {
  constructor() {
    super();
    this.state = {};
  }

  async searchDrugs(inputValue) {
    const cleanInput = inputValue.trim();
    if (cleanInput.length === 0) {
      const response = await fetch('api/popular_searches');
      return this.mapResults(await response.json());
    } else if (cleanInput.length >= 2) {
      const response = await fetch(
        `api/search_drugs?search_text=${cleanInput}`
      );
      return this.mapResults(await response.json());
    }
  }

  mapResults(json) {
    return json.map(element => {
      return { value: element[0], label: element[0] };
    });
  }

  onSelectChange(selectedOption) {
    if (selectedOption) {
      this.setState({ tableLoading: true });
      this.props.fetchAlternativeDrugs(selectedOption.value).then(() => {
        this.setState({ tableLoading: false });
      });
    } else {
      this.props.setAlternativeDrugs([]);
    }
  }

  render() {
    return (
      <div className={'app'}>
        <h3> Similar Medication Search</h3>
        <AsyncSelect
          defaultOptions
          autoFocus
          onChange={this.onSelectChange.bind(this)}
          isClearable
          loadOptions={debounce(this.searchDrugs.bind(this))}
        />
        <hr />
        <ReactTable
          column={{
            ...ReactTableDefaults.column,
            sortable: true,
            filterable: false,
            resizable: false
          }}
          loading={this.state.tableLoading}
          columns={[{ Header: 'Results', accessor: 'name' }]}
          data={this.props.alternativeDrugs}
          defaultPageSize={10}
          className="-striped -highlight"
        />
      </div>
    );
  }
}

App.propTypes = {
  alternativeDrugs: PropTypes.array.isRequired,
  fetchAlternativeDrugs: PropTypes.func.isRequired,
  setAlternativeDrugs: PropTypes.func.isRequired
};

const mapStateToProps = state => ({
  alternativeDrugs: state.alternativeDrugs
});

export default connect(
  mapStateToProps,
  { fetchAlternativeDrugs, setAlternativeDrugs }
)(App);
