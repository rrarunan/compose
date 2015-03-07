var React = require('react');

var ServiceItem = React.createClass({
  render: function () {
    var service = this.props.service;
    return (
    <tr>
      <td>{service.name}</td>
      <td>{service.options.image}</td>
      <td>{service.options.build}</td>
      <td>{service.options.ports}</td>
      <td>{service.options.volumes}</td>
      <td>{service.volumes_from}</td>
      <td>{service.links}</td>
      <td>{service.external_links}</td>
    </tr>
    );
  }

});

module.exports = ServiceItem;
