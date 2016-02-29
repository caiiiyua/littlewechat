/**
 * Created by pp on 16/2/21.
 */

function doAnswer(answer) {
  return $.post("http://inaiping.wang/answers",
  {
    "answer": answer,
  },
  function(data, status) {
    // alert("Data:" + data + "\nStatus: " + status)
    window.location.reload()
    return data
  });
}

 $(document).ready(function() {
   $("#submit_0").click(function() {
     alert("submit_0 was clicked")
     doAnswer(0);
   });
   $("#submit_1").click(function() {
     alert("submit_1 was clicked")
     doAnswer(1);
   });
 });
