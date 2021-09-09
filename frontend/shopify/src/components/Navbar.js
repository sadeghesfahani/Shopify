import React, {Component} from 'react';
import {Link,BrowserRouter as Router} from "react-router-dom";

class Navbar extends Component {
    constructor(props) {
        super(props);
        this.state = {menuMap: {}}
    }

    compileSubMenu(parent_id) {
        for (let subMenu of this.props.menu) {
            if (subMenu.parent === parent_id) {
                return
            }
        }
    }

    mapMenu() {
        const menuMap = {...this.state.menuMap}
        for (let menu of this.props.menu) {
            if (menu.parent == null) {
                menuMap[menu.id] = []
            } else {
                menuMap[menu.parent.id].push(menu.id)
            }
        }
        this.setState({menuMap: menuMap})
    }

    hasChildren(menu) {
        return this.state.menuMap[menu.id] !== undefined && this.state.menuMap[menu.id].length !==0
    }

    compileMenu(menu, index) {
        if (menu.parent == null) {
            if (this.hasChildren(menu)) {
                return (
                    <li key={index} className="nav-item dropdown">
                        <i className="dropdown-toggle d-inline-block position-relative float-right align-self-center" style={{"lineHeight":"45px"}} id={menu.name} role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"/>
                        <Link className="nav-link d-inline-block position-relative " to={`/category/${menu.id}`} id={menu.name} >
                            {menu.name}
                        </Link>
                        <div className="dropdown-menu" aria-labelledby={menu.name}>
                            {this.state.menuMap[menu.id].map((subMenu,subIndex)=>{
                                return <Link key={subIndex} className="dropdown-item" to={`/category/${this.getSubMenu(subMenu,'id')}`}>{this.getSubMenu(subMenu,'name')}</Link>
                            })}
                        </div>
                    </li>
                )
            } else {
                return (
                        <li key={index} className="nav-item active">
                            <Link className="nav-link" to={`/category/${menu.id}`}>{menu.name} <span className="sr-only"/></Link>
                        </li>
                )
            }

        }
    }

    getSubMenu(subMenu,type){
        for (let menu of this.props.menu){
            if (menu.id===subMenu && type === 'name') return menu.name
            if (menu.id===subMenu && type === 'id') return menu.id
        }
    }
    render() {
        if (this.props.menu.length === 0) return null
        return (
            <nav className='navbar navbar-expand-lg navbar-light bg-light'>
                <Link className="navbar-brand" to={''}>something</Link>
                <button className="navbar-toggler" type="button" data-toggle="collapse"
                        data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent"
                        aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"/>
                </button>

                <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav mr-auto">
                        {this.props.menu.map((menu, index) => {
                            return this.compileMenu(menu, index)
                        })}
                    </ul>
                    <form className="form-inline my-2 my-lg-0">
                        <input className="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search"/>
                        <button className="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
                    </form>
                </div>
            </nav>
        );
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (this.props.menu.length === 0 || (prevProps.menu !== [] && prevProps.menu === this.props.menu)) return null
        this.mapMenu()
    }
}

export default Navbar;