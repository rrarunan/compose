var React = require('react');
var ServiceItem = require('./serviceitem.jsx');

var Projects = React.createClass({
  getInitialState: function() {
    return {
      name: "Loading...",
      services: []
    };
  },
  componentDidMount: function() {
  var _this = this;
    $.ajax({
      url: 'http://localhost:8000/project',
      dataType: 'json',
      success: function(project) {
        this.setState({
          name: project.name,
          services: project.services
        });
      }.bind(this),
      error: function(xhr, status, err) {
        console.error('http://localhost:8000/project', status, err.toString());
      }.bind(this)
    });
  },
  render: function () {
    var name = this.state.name;

    var services = this.state.services.map(function(service) {
      return (
        <ServiceItem service={service} />
      );
    });
    return (
      <div>
        <h4>Project Name: {name}</h4>
        <hr />
        <h4>Services</h4>
        <table class="twelve">
          <thead>
            <tr>
              <th>Name</th>
              <th>Image</th>
              <th>Build</th>
              <th>Ports</th>
              <th>Volumes</th>
              <th>Volumes From</th>
              <th>Links</th>
              <th>External Links</th>
            </tr>
          </thead>
          <tbody>
            {services}
          </tbody>
        </table>
      </div>
    );
  }
});

module.exports = Projects;
