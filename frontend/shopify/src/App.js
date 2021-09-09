import './App.css';
import Navbar from "./components/Navbar";
import React, {Component} from 'react';
import {BrowserRouter, Router, Route, Link, Switch} from "react-router-dom";
import Category from "./components/category";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {menu: []}
        this.getMenu()
    }

    async getMenu() {
        await fetch('http://127.0.0.1:8000/menu').then(response => response.json()).then(menu => this.setState({menu: menu}))
    }

    render() {
        return (


<div>

            <Navbar menu={this.state.menu}/>
            <Route path='/category/:id' render={(props)=><Category {...props} category={this.state.menu}/>}/>

</div>

    )
        ;
    }
}

export default App;

