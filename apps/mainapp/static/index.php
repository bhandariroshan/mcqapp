<?php include '_header.php';?>

    <div class="container">

    <div class="col-md-2 sidebar" >

        <!-- show the logged in users account --> 
        <div id="account_info">
        
        <div class="clearfix" style="margin-bottom: 10px;">
          <!-- twitter 78px image - 'large' -->
          <!--https://dev.twitter.com/docs/user-profile-images-and-banners -->
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_normal.png"  />

          <div class="content">
            <h4 style="margin:0;">Sujit Maharjan</h4>
            <small><a href="#" class="text-muted">Edit your profile</a></small>
          </div>
        </div>
         
        <p><a href="#">Trade connections <span class="badge pull-right">42</span></a></p>
        <p><a href="#">Foods <span class="badge pull-right">35</span></a></p>
        <p><a href="#">Organisations <span class="badge pull-right">4</span></a></p>
        <p><a href="#">Awards <span class="badge pull-right">42</span></a></p>
        
          
          <!-- PUT EMPTY ONES AT THE BOTTOM OF THE LIST -->
          <!-- if ZERO ON ANY OF THESE -->
        
        <div class="alert alert-info small"> 
          <p><b>Want a great profile?</b></p> 
         
            <a href="#">Add Awards</a>
            <br />
            <a href="#">Add Organisations</a>
        </div>
         
        </div><!-- /account_info -->
 
 
    <hr /> 

      <h4>Who's nearby</h4>
 

        <p><a href="#">Individuals <span class="badge pull-right">273</span></a></p>
        <p><a href="#">Businesses <span class="badge pull-right">38</span></a></p> 

     <!--    <div class="clearfix"> 
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="https://pbs.twimg.com/profile_images/378800000006142190/2892beb0a4ee730cb98173e5d8660816_normal.jpeg" />
          <div class="content">
            <h6 style="margin:0;">Marriott Hotels</h6>
            <button type="button" class="btn btn-default btn-xs">Connect</button>
          </div>
        </div>
<hr />
        <div class="clearfix"> 
          <img class="pull-left img-rounded" style="margin:0 8px 0 0; width:30px"  src="https://pbs.twimg.com/profile_images/1241297538/C-square_normal.gif" />
          <div class="content">
            <h5 style="">City Chef</h5>
            <button type="button" class="btn btn-default btn-xs">Connect</button>
          </div>
        </div>
 -->
    
    <div class="foodtrade-sidebar">

    <hr />

    <div class="alert alert-success">If a search term is set, then show the filters below, and remove everything above up until "Edit your profile"</div>
    <hr>
     
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter by food">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Foods</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Bread </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Cheese</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Vegetables </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Ham</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> Milk</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

     <hr>
 
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter Business Type">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Businesses</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Wholesaler </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Farmer</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Caterer </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">University</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Abbatoir</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

    <hr />
     
    <!-- consider using this for search filter http://harvesthq.github.io/chosen/ -->
    <form role="form">
      <div class="form-group"> 
        <input type="email" class="form-control" id="filter_organisation" placeholder="Filter organisation">
      </div>
    </form>


    <ul class="foodtrade-tag-list">
    <li data-id="ALL" class="foodtrade-tag foodtrade-tag-click foodtrade-tag-all"><div class="foodtrade-tag-checkbox-column"><input type="checkbox" checked="checked" aria-label="All Partners" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">All Organisations</div><div class="foodtrade-tag-count">51</div></li><li data-id="8" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Johns Hopkins " class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Soil Association </div><div class="foodtrade-tag-count">6</div></li><li data-id="1" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Stanford University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">NFU</div><div class="foodtrade-tag-count">5</div></li><li data-id="16" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="École Polytechnique Fédérale de Lausanne" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Plunkett Foundation </div><div class="foodtrade-tag-count">4</div></li><li data-id="4" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="Princeton University" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text">Organic institute</div><div class="foodtrade-tag-count">3</div></li><li data-id="15" class="foodtrade-tag foodtrade-tag-click "><div class="foodtrade-tag-checkbox-column"><input type="checkbox" aria-label="University of Washington" class="foodtrade-tag-checkbox"></div><div class="foodtrade-tag-text"> Slow Food</div><div class="foodtrade-tag-count">3</div></li><li class="foodtrade-tag-showmore">show more</li>
    </ul>

    </div>
    </div>

    <div class="col-md-5">

      <!-- new item -->
 
          <input class="form-control input-lg" type="text" placeholder="Want to #buy #apples? Or #sell 30 tonnes #oats? "> 
        <hr />


      <!-- /new item -->


      <article class="activity clearfix">

        <img class="pull-left img-rounded" style="width:40px" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_normal.png"  />
        
        <div class="content">
  
         <div class="btn-group pull-right">
            <button type="button" class="btn btn-default dropdown-toggle btn-xs pull-left" data-toggle="dropdown">
              <i class="fa fa-link"></i>
              Connect <span class="caret"></span>
            </button> 
            <ul class="dropdown-menu" role="menu">
              <li><a href="#">I buy from</a></li>
              <li><a href="#">I sell to</a></li> 
              <li class="divider"></li>
              <li><a href="#">Follow on twitter</a></li>
              <li><a href="#">Like on facebook</a></li>
            </ul>
          </div> 



          <h4><a href="#">Smales Farm</a></h4>

          <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
          

          <div class="meta small muted">
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow"></i> 87.2 miles  &middot;
            <!--  // if logged in or you've allows html5 browser location -->

            <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions">78 Example Street, Test Town</a>  


            <i class="fa fa-flag"></i>
            <a class="pull-right" href="single_update.php">21m</a> 
          </div> 

          <div style="margin-top: 10px;"> 
            <a href="#" class="btn btn-primary btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-reply"></i> Reply</a>

            <!-- admin only!! --> 
            <a href="#" class="btn btn-danger btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-trash-o"></i></a> 
            <!-- // admin only!! --> 
        
            
          <div class="icons pull-right">
            <a href="#"><i class="fa fa-facebook-square"></i></a>
            <a href="#"><i class="fa fa-twitter-square"></i></a> 
            <a href="#"><i class="fa fa-phone-square"></i></a> 
            <a href="#"><i class="fa fa-rss-square"></i></a> 
            <a href="#"><i class="fa fa-envelope"></i></a> 
            <a href="#"><i class="fa fa-globe"></i></a> 
            <a href="#"><i class="fa fa-linkedin-square"></i></a> 
          </div> 
            
          </div> 
         

        </div><!-- content -->

        

      </article>

      <article class="activity clearfix">

        <img class="pull-left img-rounded" style="width:40px" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_normal.png"  />
        
        <div class="content">
  
         <div class="btn-group pull-right">
            <button type="button" class="btn btn-default dropdown-toggle btn-xs pull-left" data-toggle="dropdown">
              <i class="fa fa-link"></i>
              Connect <span class="caret"></span>
            </button> 
            <ul class="dropdown-menu" role="menu">
              <li><a href="#">I buy from</a></li>
              <li><a href="#">I sell to</a></li> 
              <li class="divider"></li>
              <li><a href="#">Follow on twitter</a></li>
              <li><a href="#">Like on facebook</a></li>
            </ul>
          </div> 



          <h4><a href="#">Smales Farm</a></h4>

          <p>Nullam quis risus eget urna mollis ornare vel eu leo. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nullam id dolor id nibh ultricies vehicula.</p>
          

          <div class="meta small muted">
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow"></i> 87.2 miles  &middot;
            <!--  // if logged in or you've allows html5 browser location -->

            <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions">78 Example Street, Test Town</a>  


            <i class="fa fa-flag"></i>
            <a class="pull-right" href="single_update.php">21m</a> 
          </div> 

          <div style="margin-top: 10px;"> 
            <a href="#" class="btn btn-primary btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-reply"></i> Reply</a>

            <!-- admin only!! --> 
            <a href="#" class="btn btn-danger btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-trash-o"></i></a> 
            <!-- // admin only!! --> 
        
            
          <div class="icons pull-right">
            <a href="#"><i class="fa fa-facebook-square"></i></a>
            <a href="#"><i class="fa fa-twitter-square"></i></a> 
            <a href="#"><i class="fa fa-phone-square"></i></a> 
            <a href="#"><i class="fa fa-rss-square"></i></a> 
            <a href="#"><i class="fa fa-envelope"></i></a> 
            <a href="#"><i class="fa fa-globe"></i></a> 
            <a href="#"><i class="fa fa-linkedin-square"></i></a> 
          </div> 
            
          </div> 
         

        </div><!-- content -->

        

      </article>

      <!-- write in the well below the article when the Reply button is clicked -->

        <div class="well well-sm"> 
          <input class="form-control input-sm" type="text" placeholder="Reply to @smalesfarm">
        </div>

      <article class="business clearfix"> 

        <img class="pull-left img-rounded" style="width:40px" src="http://a0.twimg.com/profile_images/2596092158/afpecvf41m8f0juql78p_normal.png"  />
        
        <div class="content">
  
         <div class="btn-group pull-right">
            <button type="button" class="btn btn-default dropdown-toggle btn-xs pull-left" data-toggle="dropdown">
              <i class="fa fa-link"></i>
              Connect <span class="caret"></span>
            </button> 
            <ul class="dropdown-menu" role="menu">
              <li><a href="#">I buy from</a></li>
              <li><a href="#">I sell to</a></li> 
              <li class="divider"></li>
              <li><a href="#">Follow on twitter</a></li>
              <li><a href="#">Like on facebook</a></li>
            </ul>
          </div> 



          <h4><a href="#">Smales Farm</a></h4>

          <p>Nullam quis risus eget urna mollis ornare vel eu leo. </p>
          

          <div class="meta small muted">
            <!-- if logged in or you've allows html5 browser location -->
            <i class="fa fa-location-arrow"></i> 87.2 miles  &middot;
            <!--  // if logged in or you've allows html5 browser location -->

            <a href="http://maps.google.com/maps?saddr=current+location&daddr=Sydney+Opera+House,+Sydney+Opera+House,+Bennelong+Point,+Sydney+NSW+2000,+Australia" target="_blank" data-placement="top" data-toggle="tooltip" title="Get directions">78 Example Street, Test Town</a>  


            <i class="fa fa-flag"></i>
            <a class="pull-right" href="single_update.php">21m</a> 
          </div> 

          <div style="margin-top: 10px;"> 
            <a href="#" class="btn btn-primary btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-reply"></i> Reply</a>

            <!-- admin only!! --> 
            <a href="#" class="btn btn-danger btn-xs pull-left" style="margin-right: 5px;"><i class="fa fa-trash-o"></i></a> 
            <!-- // admin only!! --> 
        
            
          <div class="icons pull-right">
            <a href="#"><i class="fa fa-facebook-square"></i></a>
            <a href="#"><i class="fa fa-twitter-square"></i></a> 
            <a href="#"><i class="fa fa-phone-square"></i></a> 
            <a href="#"><i class="fa fa-rss-square"></i></a> 
            <a href="#"><i class="fa fa-envelope"></i></a> 
            <a href="#"><i class="fa fa-globe"></i></a> 
            <a href="#"><i class="fa fa-linkedin-square"></i></a> 
          </div> 
            
          </div> 
         

        </div><!-- content -->

        

      </article>


      <article class="organisation">
        
      </article> 
      <article class="individual">
        
      </article>
    </div>

    <div class="col-md-5">

    <!-- FIX THE MAP POSITION SO IT DOES NOT SCROLL --> 
      <div style="width:100%; height: 1000px; background: #34B9D4; padding:20px"  data-spy="affix" data-offset-top="30">
        <h1>Map</h1>
      </div>
    </div>

    </div>


 <?php include '_footer.php';?>
