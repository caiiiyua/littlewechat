/**
 * Created by pp on 16/2/21.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';
import Question from './components/question/index';
import TestButton from './components/test/index';

const {Button} = WeUI;

class App extends React.Component {
    render() {
        return (
          <TestButton/>
          // <Question/>
        );
    }
};

ReactDOM.render((
    <App/>
), document.getElementById('content'));
