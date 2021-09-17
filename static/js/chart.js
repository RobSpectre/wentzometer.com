var getJSON = function(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'json';
    xhr.onload = function() {
      var status = xhr.status;
      if (status === 200) {
        callback(null, xhr.response);
      } else {
        callback(status, xhr.response);
      }
    };
    xhr.send();
};

getJSON('/snap_count', function(err, data) {
  if (err !== null) {
    console.log("Epic fail.");
  } else {
    if (data.snap_percentage <= 65) {
      document.getElementById("result").innerHTML = "Nope. This is fucked.";
    } else if (data.snap_percentage <= 75) {
      document.getElementById("result").innerHTML = "No. Carson needs to play more.";
    } else if (data.snap_percentage <= 85) {
      document.getElementById("result").innerHTML = "Yes, but it's getting critical.";
    } else if (data.snap_percentage <= 90) {
      document.getElementById("result").innerHTML = "Yes, but I'm concerned.";
    } else {
      document.getElementById("result").innerHTML = "Yes.";
    }
    var chart = c3.generate({
      bindto: "#chart",
      data: {
        columns: [
          ['Total Snaps Played', data.snap_percentage] 
        ],
        type: 'gauge'
      },
      color: {
        pattern: ['#FF0000', '#F97600', '#F6C600', '#004C54'], // the three color levels for the percentage values.
        threshold: {
          values: [65, 75, 85, 90]
        }
      },
      size: {
        height: 400 
      }
    });
  } 
});

