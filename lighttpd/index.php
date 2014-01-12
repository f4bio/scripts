
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
        <title>Lighttpd traffic &amp; requests</title>
        <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
        <meta http-equiv="content-style-type" content="text/css">
        <style type="text/css">
<!--
        div { text-align:center; }
        img { width:693px; height:431px; }
-->
        </style>
</head>

<body>
        <?php
                $lastrun = file_get_contents("./lastrun.txt");
                echo("<div>");
                echo("<h2>Lastrun: ".$lastrun."</h2>");
                echo("</div>");
        ?>
    <div>
        <h2>Lighttpd Traffic</h2>
        <img src="lighttpd-traffic-hour.png"   alt="graph1"><br>
        <img src="lighttpd-traffic-day.png"    alt="graph2"><br>
        <img src="lighttpd-traffic-month.png"  alt="graph3"><br>
    </div>
    <div>
        <h2>Lighttpd Requests</h2>
        <img src="lighttpd-requests-hour.png"  alt="graph4"><br>
        <img src="lighttpd-requests-day.png"   alt="graph5"><br>
        <img src="lighttpd-requests-month.png" alt="graph6"><br>
    </div>
  </body>
</html>
