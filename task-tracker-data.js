(function (root, factory) {
  const data = factory();
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = data;
  } else {
    root.TikTok_TASK_TRACKER_DATA = data;
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  return {
    countries: {
      "cn": "China",
      "jp": "Japan",
      "au": "Australia",
      "my": "Malaysia",
      "id": "Indonesia",
      "in": "India",
      "sg": "Singapore",
      "hk": "Hong Kong",
      "th": "Thailand",
      "vn": "Vietnam"
},
    seeds: {
      "cn": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "jp": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "au": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "my": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "id": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "in": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "sg": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "hk": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "th": {
            "nextId": 1,
            "tasks": [],
            "history": []
      },
      "vn": {
            "nextId": 1,
            "tasks": [],
            "history": []
      }
},
  };
});
