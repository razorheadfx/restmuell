RESTMuell 
=========

RESTMuell or rather Restmüll is a primitive shell wrapper for [Fuck off As A Service](https://foaas.com)'s REST API.
At runtime, the API's [rudimentary self description](https://foaas.com/operations) is requested and parsed. Then methods are generated based on the description which are used to provide a simple command line to make calls to the API.
-------------------------------
Thanks very much to @yassya for the idea and help unleashing Python's first-class-object magic along the way (think triple ').
-------------------------------
TODO:
- [x] added classes, license and README
- [ ] check whether number of arguments is sufficient for the given operation
- [ ] push falsly used methods and error traces to [/dev/null As A Service](https://devnull-as-a-service.com) as JSON objects ('cos who wants to read them locally anyways?)