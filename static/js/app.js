/**
 * Created by pp on 16/2/21.
 */
'use strict'

var React = require('react')

class Hello extends React.Component {
    render() {
        return (
          <h2>Hello React</h2>
        );
    }
}

React.render(<Hello/>, document.getElementById('content2'));