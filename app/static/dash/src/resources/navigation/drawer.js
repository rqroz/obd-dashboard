export default {
  auth: [
    {
      icon: 'mdi-view-dashboard',
      label: 'Control Panel',
      route: { name: 'Dashboard' },
    },
    {
      icon: 'mdi-steering',
      label: 'Driver Profiling',
      route: { name: 'DriverProfile' },
    },
    {
      icon: 'mdi-chart-bell-curve',
      label: 'Line Charts',
      route: { name: 'LineChart' },
    },
  ],
  unauth: [
    {
      icon: 'mdi-home',
      label: 'Home',
      route: { name: 'Index' },
    },
  ],
};
