"use strict";

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';

const {Button, Icon, Article, Cells, CellsTitle, CellsTips, Cell, CellHeader, CellBody, CellFooter} = WeUI;

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

            <CellsTitle>带说明的列表项</CellsTitle>
            <Cells>
                <Cell>
                    <CellBody>
                        标题文字
                    </CellBody>
                    <CellFooter>
                        说明文字
                    </CellFooter>
                </Cell>
            </Cells>

            <CellsTitle>带说明、跳转的列表项</CellsTitle>
            <Cells access>
                <Cell href="javascript:;">
                    <CellBody>
                        标题文字
                    </CellBody>
                    <CellFooter>
                        说明文字
                    </CellFooter>
                </Cell>
                <Cell>
                    <CellBody>
                        标题文字
                    </CellBody>
                    <CellFooter>
                        说明文字
                    </CellFooter>
                </Cell>
            </Cells>
          </section>
        );
    }
};
