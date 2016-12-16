import {Button, Icon, Card} from 'react-materialize';
import React from 'react';
import ReactDOM from 'react-dom';
import RMAT from 'react-materialize';


var ProductCards = React.createClass({
  // sets initial state
  getInitialState: function(){
    return { productSelected: '' };
  },

  // sets state, triggers render method
  handleChange: function(event){
    this.setState({productSelected:event.target.value});
  },

  ListItem: function(props) {  
    return (
	<div className="card hoverable black inline" id={props.value}>
	<div className="card-image">
	<img src={"../../static/img/"+ props.value +".png"}></img>
	</div>
	<span className="card-title white-text">{props.value}</span>
	</div>);
  },

  productList: function(props) {
	  var products = this.props.products;
      console.log(props);
	  console.log(products);
	  return (
		<div>
		  {products.map((product) =>
			<this.ListItem key={product.key}
					  value={product.name.toString()} />
		  )}
		</div>
	  );
	},

  render: function(props) {
    var products = this.props.products;
    return (this.productList(products));
    //var productSelected = this.state.productSelected.trim().toLowerCase();

    }
  //return (
  //      <ul>
  //        {products.map(function(listValue, i){
  //          return <div className="card hoverable  blue-grey darken-1 inline">
  //                <div className="card-image">
  //            </div>
  //          <span key={i} className="card-title white-text"> {listValue.name}</span>
  //          </div>
  //              }
  //          )}
  //      </ul>
  //    )}
});

      
//var ProductSelection = React.createClass({
// <img  key={i} src="../../static/img/" + {listValue.name} + '.png'>//  // sets initial state
//  getInitialState: function(){
//    return { productSelected: '' };
//  },
//
//  // sets state, triggers render method
//  handleChange: function(event){
//    this.setState({productSelected:event.target.value});
//    console.log("scope updated!");
//  },
//
//  render: function() {
//
//    var products = this.props.items;
//    var productSelected = this.state.productSelected.trim().toLowerCase();
//
//    return (
//	  <div class='outer'>
//	  <div class="row">
//	  <div class="col m4">
//		<div class="card">
//		  <div class="card-image">
//			<img src="http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"/>
//			<span class="card-title" style="width:100%; background: rgba(0, 0, 0, 0.5);">Sample1</span>
//		  </div>
//		  <div class="card-content">
//			<p>I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.</p>
//		  </div>
//		  <div class="card-action">
//			<a href="#">This is a link</a>
//		  </div>
//		</div>
//	  </div>
//	  <div class="col m4">
//		<div class="card">
//		  <div class="card-image">
//			<img src="http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"/>
//			<span class="card-title" style="width:100%; background: rgba(0, 0, 0, 0.5);">Sample2</span>
//		  </div>
//		  <div class="card-content">
//			<p>I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.</p>
//		  </div>
//		  <div class="card-action">
//			<a href="#">This is a link</a>
//		  </div>
//		</div>
//	  </div>
//	</div>
//
//	<div class="fixed-action-btn click-to-toggle" style="bottom: 45px; right: 24px;">
//	  <a class="btn-floating btn-large red">
//		<i class="large material-icons">menu</i>
//	  </a>
//	  <ul>
//		<li><a class="btn-floating red" class="fbtn" href="test.html"><i class="material-icons">home</i></a></li>
//		<li><a class="btn-floating yellow darken-1" class="fbtn" href="#"><i class="material-icons">work</i></a></li>
//		<li><a class="btn-floating green" class="fbtn" href="about.html"><i class="material-icons">account_circle</i></a></li>
//		<li><a class="btn-floating blue" class="fbtn" href="contact.html"><i class="material-icons">speaker_notes</i></a></li>
//	  </ul>
//	</div>
//	<div class="clear" style="clear:both; height: 100px;">
//	</div>
//	</div>
//   ) 
//  }
//});

//var CompanySearch = React.createClass({
//
//  // sets initial state
//  getInitialState: function(){
//    return { searchString: '' };
//  },
//
//  // sets state, triggers render method
//  handleChange: function(event){
//    // grab value form input box
//    this.setState({searchString:event.target.value});
//    console.log("scope updated!");
//  },
//
//  render: function() {
//
//    var companies = this.props.items;
//    var searchString = this.state.searchString.trim().toLowerCase();
//
//    // filter companies list by value from input box
//    if(searchString.length > 0){
//      companies = companies.filter(function(company){
//        return company.name.toLowerCase().match( searchString );
//      });
//    }
//
//    return (
//      <div>
//        <input type="text" value={this.state.searchString} onChange={this.handleChange} placeholder="Type a company name" />
//        <ul>
//          { companies.map(function(company){ return <li>{company.name} </li> }) }
//        </ul>
//      </div>
//    )
//  }
//
//});

// list of companies, defined with JavaScript object literals



var products = [
  {"key": 1, "name": "Mortgage"},
  {"key": 2, "name": "Debt collection"},
  {"key": 3, "name": "Credit reporting"},
  {"key": 4, "name": "Credit card"},
  // {"key": 5, "name": "Bank account or service"},
  {"key": 6, "name": "Consumer Loan"}
  ];

// const ProductCards = products.map((product)
//   <div key = {product.name} className="card hoverable  blue-grey darken-1 inline">
//       <div key = {product.name} className="card-image">
//     <img  key = {product.name} src="../../static/img/" + {product.name} + '.png'>
//   </div>
// <span  key = {product.name} className="card-title white-text"> {product.name}</span>
// </div>
//     );

//var companies = [
//  {"name": "Sweden"}, {"name": "China"}, {"name": "Peru"}, {"name": "Czech Republic"},
//  {"name": "Bolivia"}, {"name": "Latvia"}, {"name": "Samoa"}, {"name": "Armenia"},
//  {"name": "Greenland"}, {"name": "Cuba"}, {"name": "Western Sahara"}, {"name": "Ethiopia"},
//  {"name": "Malaysia"}, {"name": "Argentina"}, {"name": "Uganda"}, {"name": "Chile"},
//  {"name": "Aruba"}, {"name": "Japan"}, {"name": "Trinidad and Tobago"}, {"name": "Italy"},
//  {"name": "Cambodia"}, {"name": "Iceland"}, {"name": "Dominican Republic"}, {"name": "Turkey"},
//  {"name": "Spain"}, {"name": "Poland"}, {"name": "Haiti"}
//];

// ReactDOM.render(
//   <ul> {ProductCards} </ul>,
//   document.getElementById('product_cards')
// );


ReactDOM.render(
  <ProductCards products={products} />,
  document.getElementById('product_cards')
);

//ReactDOM.render(
//  <CompanySearch items={ companies } />,
//  document.getElementById('company-container')
//);
