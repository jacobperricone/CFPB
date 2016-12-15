(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
var ProductSelection = React.createClass({displayName: "ProductSelection",

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
	  React.createElement("div", {class: "outer"}, 
	  React.createElement("div", {class: "row"}, 
	  React.createElement("div", {class: "col m4"}, 
		React.createElement("div", {class: "card"}, 
		  React.createElement("div", {class: "card-image"}, 
			React.createElement("img", {src: "http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"}), 
			React.createElement("span", {class: "card-title", style: "width:100%; background: rgba(0, 0, 0, 0.5);"}, "Sample1")
		  ), 
		  React.createElement("div", {class: "card-content"}, 
			React.createElement("p", null, "I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.")
		  ), 
		  React.createElement("div", {class: "card-action"}, 
			React.createElement("a", {href: "#"}, "This is a link")
		  )
		)
	  ), 
	  React.createElement("div", {class: "col m4"}, 
		React.createElement("div", {class: "card"}, 
		  React.createElement("div", {class: "card-image"}, 
			React.createElement("img", {src: "http://www.ilikewallpaper.net/ipad-wallpapers/download/2268/Square-Pattern-ipad-wallpaper-ilikewallpaper_com.jpg"}), 
			React.createElement("span", {class: "card-title", style: "width:100%; background: rgba(0, 0, 0, 0.5);"}, "Sample2")
		  ), 
		  React.createElement("div", {class: "card-content"}, 
			React.createElement("p", null, "I am a very simple card. I am good at containing small bits of information. I am convenient because I require little markup to use effectively.")
		  ), 
		  React.createElement("div", {class: "card-action"}, 
			React.createElement("a", {href: "#"}, "This is a link")
		  )
		)
	  )
	), 

	React.createElement("div", {class: "fixed-action-btn click-to-toggle", style: "bottom: 45px; right: 24px;"}, 
	  React.createElement("a", {class: "btn-floating btn-large red"}, 
		React.createElement("i", {class: "large material-icons"}, "menu")
	  ), 
	  React.createElement("ul", null, 
		React.createElement("li", null, React.createElement("a", {class: "btn-floating red", class: "fbtn", href: "test.html"}, React.createElement("i", {class: "material-icons"}, "home"))), 
		React.createElement("li", null, React.createElement("a", {class: "btn-floating yellow darken-1", class: "fbtn", href: "#"}, React.createElement("i", {class: "material-icons"}, "work"))), 
		React.createElement("li", null, React.createElement("a", {class: "btn-floating green", class: "fbtn", href: "about.html"}, React.createElement("i", {class: "material-icons"}, "account_circle"))), 
		React.createElement("li", null, React.createElement("a", {class: "btn-floating blue", class: "fbtn", href: "contact.html"}, React.createElement("i", {class: "material-icons"}, "speaker_notes")))
	  )
	), 
	React.createElement("div", {class: "clear", style: "clear:both; height: 100px;"}
	)
	)
   ) 
  }
});

var CompanySearch = React.createClass({displayName: "CompanySearch",

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
      React.createElement("div", null, 
        React.createElement("input", {type: "text", value: this.state.searchString, onChange: this.handleChange, placeholder: "Type a company name"}), 
        React.createElement("ul", null, 
           companies.map(function(company){ return React.createElement("li", null, company.name, " ") }) 
        )
      )
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
  React.createElement(ProductSelection, {items:  products }),
  document.getElementById('product-container')
);

ReactDOM.render(
  React.createElement(CompanySearch, {items:  companies }),
  document.getElementById('company-container')
);

},{}]},{},[1]);

},{}]},{},[1]);
