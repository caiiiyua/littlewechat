/**
 * Created by pp on 16/2/21.
 */
'use strict';

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';
import Question from './components/question/index';
import TestButton from './components/test/index';

const {Button} = WeUI;
const a = document.getElementById('init_state').innerHTML;
// const b = JSON.parse(a);

class App extends React.Component {
    render() {
        return (
          // <TestButton/>
          // <Button> {a}</Button>
          <Question />
        );
    }
};

ReactDOM.render((
    <App/>
), document.getElementById('content'));
