import './App.css';
import Navbar from "./components/Navbar";
import React, {Component} from 'react';
import {BrowserRouter as Router, Route, Link, Switch} from "react-router-dom";
import Category from "./components/category";
import Register from "./components/Register";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            menu: [],
            submenu: [],
            user: null
        }
        this.getMenu()
    }


    async getMenu() {
        await fetch('http://127.0.0.1:8000/category/roots/').then(response => response.json()).then(roots => this.generateMenuTree(roots))

    }

    async generateMenuTree(roots) {
        this.setState({menu: roots})
        for (let root of roots) {
            fetch(`http://127.0.0.1:8000/category/${root.id}/children/`).then(response => response.json()).then(submenu => this.fillMenuData(root.id, submenu))
        }
    }

    fillMenuData(root_id, submenu) {
        const menu = {...this.state.submenu}
        menu[root_id] = submenu
        this.setState({submenu: menu})
    }

    render() {
        return (

            <Router>
                <div>
                    <Navbar menu={this.state.menu} submenu={this.state.submenu}/>
                    <Switch>
                        <Route path="/register">
                            <Register/>
                        </Route>
                    </Switch>
                </div>
            </Router>

        )
    }

    componentDidMount() {
        const user = localStorage.getItem('user')
        this.setState({user: user})
    }
}

export default App;

