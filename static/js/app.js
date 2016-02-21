/**
 * Created by pp on 16/2/21.
 */
<script type="text/jsx">

      /*** @jsx React.DOM */

      var helloWorld2 = React.createClass({
        render: function() {
          return (<h1>Greetings, from Hello Another world!</h1>)
        }
      });

      React.render(
        React.createElement(helloWorld2, null),
        document.getElementById('content2')
      );
</script>