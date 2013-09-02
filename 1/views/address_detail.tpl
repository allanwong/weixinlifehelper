<!DOCTYPE html> 
<html> 
  <head> 
    <title>地址信息详细</title> 
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
    <p><label>标签:</label><span>{{ result["detail_info"]["tag"] }}</span></p>
    <p>
      <label>步行</label>
      <ul>
	% for step in line_result["routes"][0]["steps"]:
	<li>
	{{ step["instructions"].replace("<b>","").replace("</b>","") }}	    
	</li>
	% end
      </ul>      
    </p>
    <p><a href="{{ result["detail_info"]["detail_url"] }}">点击查看详细</a></p>    
  </body>
</html>
