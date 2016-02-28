/**
 * Created by pp on 16/2/21.
 */

function doAnswer(answer) {
  return $.post("inaiping.wang/answers",
  {
    "answer": answer,
  },
  function(data, status) {
    alert("Data:" + data + "\nStatus: " + status)
    return data
  });
}

 $(document).ready(function() {
   $("#submit_0").click(function() {
     doAnswer(0);
   });
   $("#submit_1").click(function() {
     doAnswer(1);
   });
 });
