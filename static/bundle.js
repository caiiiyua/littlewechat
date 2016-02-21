/**
 * Created by pp on 16/2/21.
 */

<script type="text/jsx">

      /*** @jsx React.DOM */

      var helloWorld = React.createClass({
        render: function() {
          return (<h2>Greetings, from Real Python!</h2>)
        }
      })

      React.render(
        React.createElement(helloWorld, null),
        document.getElementById('content2')
      )
</script>;