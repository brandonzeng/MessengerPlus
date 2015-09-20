if (Meteor.isClient) {
  window.processFile = function () {
    var files = document.getElementById('attachment').files;
    console.log(files)
  }
}

if (Meteor.isServer) {
}
