class Place {
    constructor(name, x, y, tokens = 0) {
      this.name = name;
      this.x = x;
      this.y = y;
      this.tokens = tokens;
    }
  
    addTokens(count = 1) {
      this.tokens += count;
    }
  
    removeTokens(count = 1) {
      if (this.tokens >= count) {
        this.tokens -= count;
      }
    }
  }
  
  class Transition {
    constructor(name, x, y, inputPlaces, outputPlaces) {
      this.name = name;
      this.x = x;
      this.y = y;
      this.inputPlaces = inputPlaces;
      this.outputPlaces = outputPlaces;
    }
  
    canFire() {
      return this.inputPlaces.every(place => place.tokens > 0);
    }
  
    fire() {
      if (this.canFire()) {
        this.inputPlaces.forEach(place => place.removeTokens());
        this.outputPlaces.forEach(place => place.addTokens());
      }
    }
  }
  
  class PetriNet {
    constructor(svg) {
      this.places = {};
      this.transitions = {};
      this.svg = svg;
    }
  
    addPlace(name, x, y, tokens = 0) {
      const place = new Place(name, x, y, tokens);
      this.places[name] = place;
  
      this.svg.append("g")
        .attr("class", "place")
        .attr("id", name)
        .append("circle")
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 30);
    }
  
    addTransition(name, x, y, inputPlaces, outputPlaces) {
      const transition = new Transition(
        name,
        x,
        y,
        inputPlaces.map(ip => this.places[ip]),
        outputPlaces.map(op => this.places[op])
      );
      this.transitions[name] = transition;
  
      this.svg.append("g")
        .attr("class", "transition")
        .attr("id", name)
        .append("rect")
        .attr("x", x - 15)
        .attr("y", y - 30)
        .attr("width", 30)
        .attr("height", 60);
    }
  
    drawLinks() {
      Object.values(this.transitions).forEach(transition => {
        transition.inputPlaces.forEach(input => {
          this.svg.append("line")
            .attr("class", "link")
            .attr("x1", input.x)
            .attr("y1", input.y)
            .attr("x2", transition.x)
            .attr("y2", transition.y);
        });
  
        transition.outputPlaces.forEach(output => {
          this.svg.append("line")
            .attr("class", "link")
            .attr("x1", transition.x)
            .attr("y1", transition.y)
            .attr("x2", output.x)
            .attr("y2", output.y);
        });
      });
    }
  
    drawTokens() {
      this.svg.selectAll(".token-text").remove();
      Object.values(this.places).forEach(place => {
        this.svg.append("text")
          .attr("class", "token-text")
          .attr("x", place.x)
          .attr("y", place.y + 5)
          .attr("text-anchor", "middle")
          .style("font-size", "16px")
          .text(place.tokens);
      });
    }
  
    runTransition(name) {
      if (this.transitions[name]?.canFire()) {
        this.transitions[name].fire();
      }
    }
  }
  
  // Initialize simulation
  const svg = d3.select("#graph");
  svg.append("defs").append("marker")
    .attr("id", "arrow")
    .attr("viewBox", "0 0 10 10")
    .attr("refX", 10)
    .attr("refY", 5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("d", "M 0 0 L 10 5 L 0 10 Z")
    .attr("fill", "black");
  
  const petriNet = new PetriNet(svg);
  petriNet.addPlace("queue", 100, 200, 5);
  petriNet.addPlace("processor", 300, 200, 0);
  petriNet.addPlace("completed", 500, 200, 0);
  petriNet.addTransition("process", 200, 200, ["queue"], ["processor"]);
  petriNet.addTransition("complete", 400, 200, ["processor"], ["completed"]);
  petriNet.drawLinks();
  
  function simulate(fullTime, interval) {
    let time = 0;
  
    function step() {
      // Populating the queue
      if (Math.random() < 0.3) { // Вероятность 30% на каждом шаге
        petriNet.places["queue"].addTokens(Math.floor(Math.random() * 3) + 1); // Добавляем от 1 до 3 токенов
      }
  
      // Process queue to processor
      if (time % 3 === 0) {
        petriNet.runTransition("process");
      }
  
      // Complete processing
      if (time % 5 === 0) {
        petriNet.runTransition("complete");
      }
  
      // Draw tokens
      petriNet.drawTokens();
  
      // Update time
      time++;
      if (time < fullTime) {
        setTimeout(step, interval);
      }
    }
  
    step();
  }
  
  simulate(100, 500);
  