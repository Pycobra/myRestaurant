
export default class {
    mainHttp = "insideout.com";
    Constructor(httpName1, httpAge1){
        this.httpName1 = httpName1;
        this.httpAge1 = httpAge1;
    }
    requestHandler() {
        console.log('(' + this.httpName1, this.httpAge1 + ')', this.mainHttp)
        this.radar()
    }
    radar() {
        console.log("your  location  is  being  bogged  down......")
    }

}


