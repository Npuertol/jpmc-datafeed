import React, { Component } from 'react';
import { Table } from '@jpmorganchase/perspective';
import { ServerRespond } from './DataStreamer';
import { DataManipulator } from './DataManipulator';
import './Graph.css';

interface IProps {
  data: ServerRespond[],
}

interface PerspectiveViewerElement extends HTMLElement {
  load: (table: Table) => void,
}
class Graph extends Component<IProps, {}> {
  table: Table | undefined;

  render() {
    return React.createElement('perspective-viewer');
  }

  componentDidMount() {
    // Get element from the DOM.
    const elem = document.getElementsByTagName('perspective-viewer')[0] as unknown as PerspectiveViewerElement;

    const schema = { // took out stock, and then put in prices for stocks abc and def which will be used to calculate ratio. upper and lower bounds and trigger alert are essential to monitoring correlation between 2 stocks
      price_abc: 'float',
      price_def: 'float',
      ratio: 'float',
      timestamp: 'date',
      upper_bound: 'float',
      lower_bound: 'float',
      trigger_alert: 'float',
    };

    if (window.perspective && window.perspective.worker()) {
      this.table = window.perspective.worker().table(schema);
    }
    if (this.table) {
      // Load the `table` in the `<perspective-viewer>` DOM reference.
      elem.load(this.table);
      elem.setAttribute('view', 'y_line');
      // took column-pivots out since we do not want to visualize stocks ABC/DEF prices, but instead their ratio
      elem.setAttribute('row-pivots', '["timestamp"]');
      // columns focuses on specific part of a datapoint's data along the y-axis
      elem.setAttribute('columns', '["ratio", "lower_bound", "upper_bound", "trigger_alert"]');
      // aggregates handles duplicated data and makes them into one data point (data point is only unique if its timestamp is unique)
      elem.setAttribute('aggregates', JSON.stringify({
        price_abc: 'avg',
        price_def: 'avg',
        ratio: 'avg',
        timestamp: 'distinct count',
        upper_bound: 'avg',
        lower_bound: 'avg',
        trigger_alert: 'avg',
      }));
    }
  }

  componentDidUpdate() {
    if (this.table) { // added brackets within this.table.update(), see line 15 in DataManipulator.ts
      this.table.update([
        DataManipulator.generateRow(this.props.data),
      ]);
    }
  }
}

export default Graph;
