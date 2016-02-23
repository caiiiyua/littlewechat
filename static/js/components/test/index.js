"use strict";

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';

const {Button, Icon, Article} = WeUI;

export default class TestButton extends React.Component {
    render() {

        return (
          <section>
            <Button>按钮2</Button>
            <Button disabled>按钮</Button>
            <Button type="warn">按钮</Button>
            <Button type="warn" disabled>按钮</Button>

            <Button type="default">按钮</Button>
            <Button type="default" disabled>按钮</Button>

            <Icon size="large" value="success" />
            <Icon size="large" value="info" />
            <Icon size="large" value="warn" />
            <Icon size="large" value="waiting" />
            <Icon size="large" value="safe_success" />
            <Icon size="large" value="safe_warn" />

            <Article>
              <h1>Hello article</h1>
              <p>Glad to see you</p>
            </Article>
          </section>
        );
    }
};
