<!DOCTYPE html> 
<html> 
  <head> 
    <title>团购信息详细</title> 
    <meta name="viewport" content="width=device-width, initial-scale=1"> 
    <style type="text/css">
      p{
          margin-bottom: 20px; 
          border-bottom: 1px solid #ccc;
      }
    </style>
  </head> 
  <body>
    <p><label>名称:</label><span>{{ result["name"] }}</span></p>
    <p><label>地址:</label><span>{{ result["address"] }}</span></p>
    % for event in result["events"]:
    <ul>
      <li>
	<label>标题:</label><span>{{ event["groupon_title"] }}</span>
      </li>
      <li>
	<label>来源:</label><span>{{ event["cn_name"] }}</span>
      </li>
      <li>
	<label>原价:</label><span>{{ event["regular_price"] }}</span>
	<label>现价:</label><span>{{ event["groupon_price"] }}</span>
      </li>
      <li>
	<label>开始日期:</label><span>{{ event["groupon_start"] }}</span>
	<label>结束日期:</label><span>{{ event["groupon_end"] }}</span>
      </li>
      <li>
	<a href="{{event["groupon_url_mobile"]}}">购买</a>
      </li>
    </ul>
    % end
  </body>
</html>
