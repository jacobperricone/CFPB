var ProductSelection = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { productSelected: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    this.setState({productSelected:event.target.value});
    console.log("scope updated!");
  },

  render: function() {

    var products = this.props.items;
    var productSelected = this.state.productSelected.trim().toLowerCase();

    return (
	  <div class='outer'>
	  <div class="row">
	  <div class="col m4">
		<div class="card">
		  <div class="card-image">
			<img src="http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"/>
			<span class="card-title" style="width:100%; background: rgba(0, 0, 0, 0.5);">Sample1</span>
		  </div>
		  <div class="card-content">
			<p>I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.</p>
		  </div>
		  <div class="card-action">
			<a href="#">This is a link</a>
		  </div>
		</div>
	  </div>
	  <div class="col m4">
		<div class="card">
		  <div class="card-image">
			<img src="http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"/>
			<span class="card-title" style="width:100%; background: rgba(0, 0, 0, 0.5);">Sample2</span>
		  </div>
		  <div class="card-content">
			<p>I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.</p>
		  </div>
		  <div class="card-action">
			<a href="#">This is a link</a>
		  </div>
		</div>
	  </div>
	</div>

	<div class="fixed-action-btn click-to-toggle" style="bottom: 45px; right: 24px;">
	  <a class="btn-floating btn-large red">
		<i class="large material-icons">menu</i>
	  </a>
	  <ul>
		<li><a class="btn-floating red" class="fbtn" href="test.html"><i class="material-icons">home</i></a></li>
		<li><a class="btn-floating yellow darken-1" class="fbtn" href="#"><i class="material-icons">work</i></a></li>
		<li><a class="btn-floating green" class="fbtn" href="about.html"><i class="material-icons">account_circle</i></a></li>
		<li><a class="btn-floating blue" class="fbtn" href="contact.html"><i class="material-icons">speaker_notes</i></a></li>
	  </ul>
	</div>
	<div class="clear" style="clear:both; height: 100px;">
	</div>
	</div>
   ) 
  }
});

var CompanySearch = React.createClass({

  // sets initial state
  getInitialState: function(){
    return { searchString: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    // grab value form input box
    this.setState({searchString:event.target.value});
    console.log("scope updated!");
  },

  render: function() {

    var companies = this.props.items;
    var searchString = this.state.searchString.trim().toLowerCase();

    // filter companies list by value from input box
    if(searchString.length > 0){
      companies = companies.filter(function(company){
        return company.name.toLowerCase().match( searchString );
      });
    }

    return (
      <div>
        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Type a company name" />
        <ul>
          { companies.map(function(company){ return <li>{company.name} </li> }) }
        </ul>
      </div>
    )
  }

});

// list of companies, defined with JavaScript object literals
var products = [
  {"name": "Mortgage"},
  {"name": "Debt collection"},
  {"name": "Credit reporting"},
  {"name": "Credit card"},
  {"name": "Bank account or service"},
  {"name": "Consumer Loan"},
  {"name": "Student loan"},
  {"name": "Payday loan"},
  {"name": "Money transfers"},
  {"name": "Prepaid card"}
];
var companies = [
  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
];

ReactDOM.render(
  <ProductSelection items = { products } />,
  document.getElementById('product-container')
);

ReactDOM.render(
  <CompanySearch items={ companies } />,
  document.getElementById('company-container')
);
