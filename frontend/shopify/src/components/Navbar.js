import React, {Component} from 'react';
import {Link, BrowserRouter as Router} from "react-router-dom";
import 'react-bootstrap-icons'

class Navbar extends Component {

    constructor(props) {
        super(props);
        this.logUserOut = this.logUserOut.bind(this)
    }


    logUserOut() {
        localStorage.removeItem('user')
        localStorage.setItem('isUserLoggedIn', "0")
        this.props.handleStatus(false)
    }

    totalCard = () => {
        var total_number = 0
        if (this.props.orders.length > 1) {
            for (let order of this.props.orders) {
                total_number = total_number + order.quantity
            }
            return total_number
        } else if(this.props.orders.length ===1){
            return this.props.orders[0].quantity
        }
        return null

    }
    generateSingleOrder = () =>{
        return <div>{this.props.orders[0].name} <span className="badge badge-primary">{this.props.orders[0].quantity}</span></div>
    }

    generateCard() {
        return (
            <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id='card' role="button"
                   data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    <i className="bi bi-cart3"/><span className="badge badge-primary">{this.totalCard()}</span>
                </a>
                <div className="dropdown-menu" aria-labelledby='card'>

                    {this.props.orders && this.props.orders.length > 0 && this.props.orders.map((order, index) => {
                        return (
                            <div key={index}>{order.name} <span className="badge badge-primary">{order.quantity}</span>
                            </div>
                        )
                    })}

                    {/*{this.props.orders && this.props.orders.length === 1 && this.generateSingleOrder()}*/}
                    <Link to='/checkout' className='btn btn-primary'>سبد خرید</Link>

                </div>
            </li>
        )
    }


    render() {
        if (localStorage.getItem('isUserLoggedIn') === "1") {


        }
        if (this.props.menu.length === 0) return null
        return (
            <nav className='navbar navbar-expand-lg navbar-light bg-light'>
                <link rel="stylesheet"
                      href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css"/>
                <Link className="navbar-brand" to='#'>something</Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav ">
                        {this.props.menu.map((menu, index) => {
                            return this.compileMenu(menu, index)
                        })}
                        {this.generateAccount()}
                        {this.generateCard()}
                    </ul>
                    <form className="form-inline my-2 my-lg-0 mr-auto">
                        <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                        <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>

                </div>
            </nav>
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.menu.length === 0 || (prevProps.menu !== [] && prevProps.menu === this.props.menu)) return null

    }

    compileMenu(menu, index) {
        if (this.props.submenu[menu.id] !== undefined && this.props.submenu[menu.id].length > 0) {
            return (
                <li key={index} className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id={`navbarDropdown${index}`} role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {menu.name}
                    </a>
                    <div className="dropdown-menu" aria-labelledby={`navbarDropdown${index}`}>
                        {this.props.submenu[menu.id].map((submenu, index) => {
                            return <Link key={index} className="dropdown-item"
                                         to={`/category/${submenu.id}`}>{submenu.name}</Link>
                        })}

                    </div>
                </li>
            )
        } else {
            return (
                <li key={index} className="nav-item">
                    <Link className="nav-link" to={`/category/${menu.id}`}>{menu.name}</Link>
                </li>
            )
        }
    }

    generateAccount() {
        if (this.props.loggedIn) {
            return (
                <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id='navbarDropdown-account' role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        ناحیه کاربری
                    </a>
                    <div className="dropdown-menu" aria-labelledby='navbarDropdown-account'>
                        <Link to="#" className="dropdown-item">اطلاعات کاربری</Link>
                        <Link to="#" onClick={this.logUserOut} className="dropdown-item">خروج</Link>
                    </div>
                </li>
            )
        } else {
            return (
                <li className="nav-item dropdown">
                    <a className="nav-link dropdown-toggle" href="#" id='navbarDropdown-account' role="button"
                       data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        ناحیه کاربری
                    </a>
                    <div className="dropdown-menu" aria-labelledby='navbarDropdown-account'>
                        <Link to="/login" className="dropdown-item">ورود</Link>
                        <Link to="/register" className="dropdown-item">ثبت نام</Link>
                    </div>
                </li>
            )
        }
    }
}

export default Navbar;