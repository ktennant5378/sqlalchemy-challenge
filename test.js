class House{
    constructor(color, size, price, location){
        this.color = color;
        this.size = size;
        this.price = price;
        this.location = location;
    }
}    
const myHouse = new House('Trippie red', 'big', 'expensive', 'NYC');
console.log(myHouse); // red

const myHouse2 = new House('blue', 'small', 'cheap', 'LA');
console.log(myHouse2); // blue
