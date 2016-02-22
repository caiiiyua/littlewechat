/**
 * Created by pp on 16/2/21.
 */

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';

const {Button} = WeUI;

class App extends React.Component {
    render() {
        return (
            <Button>hello wechat</Button>
        );
    }
};

ReactDOM.render((
    <App/>
), document.getElementById('content'));
