"use strict";

import React from 'react';
import ReactDOM from 'react-dom';
import WeUI from 'react-weui';
import 'weui';

const {Button, Icon, Article, Cells, CellsTitle, CellsTips, Cell, CellHeader, CellBody, CellFooter} = WeUI;

export default class Question extends React.Component {
  render() {
    // const {title, description, creator, created_at, category, expired_at, show_answer, modify_answer} = this.props;
    const {title, creator, expired_at, description} = {
      title: "Test",
      creator: "Caiiiyua",
      expired_at: "2016-02-29",
      description: "Do u want to go to party this weekend ?"
    };
    return (
      <section>
        <div className='question_container'>
        <h2> {title} </h2>
        <h4> by {creator} expired at {expired_at} </h4>
        <Article>
          <h1>{description}</h1>
        </Article>
        <div className='button_container'>
          <Button type="primary">OK</Button>
          <Button type="warn">Deny</Button>
        </div>
        </div>
      </section>

        // <div className='question_container'>
        //   <h2> {title} </h2>
        //   <h4> by {creator} expired at {expired_at} </h4>
        //   <Article>
        //     <h1>{description}</h1>
        //   </Article>
        //
        //   <div className='button_container'>
        //     <Icon size="large" value="success_no_cicle" />
        //     <Icon size="large" value="warn_no_cicle" />
        //   </div>
        // </div>

    );
  }
};
