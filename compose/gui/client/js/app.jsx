var React = require('react');
var Router = require('react-router');
var {Route, DefaultRoute, RouteHandler, Link} = require('react-router');
var Projects = require('./projects');
var Services = require('./services');
/*<li><Link to="projectsPage">Projects</Link></li>
 /<li><Link to="servicesPage">Services</Link></li>*/
var App = React.createClass({
  render: function () {
    return (
      <div className="grid-frame vertical">
        <div className="grid-content shrink" style={{padding: 0}}>
          <ul className="primary condense menu-bar">
            <li><a><strong>Docker Compose GUI</strong></a></li>
          </ul>
        </div>
        <div className="grid-content">
            <RouteHandler />
        </div>
      </div>
    );
  }
});

var routes = (
  <Route name='app' path='/' handler={App}>
    <Route name='projectsPage' handler={Projects}/>
    <Route name='servicesPage' handler={Services}/>
    <DefaultRoute handler={Projects}/>
  </Route>
);

Router.run(routes, function (Handler) {
  React.render(<Handler />, document.body);
});
