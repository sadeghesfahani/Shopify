import React, {Component} from 'react';
import {Link} from "react-router-dom";

class Breadcumb extends Component {

    generateClass(index){
        if(index === this.props.list.length) return "breadcrumb-item active"
        return "breadcrumb-item"
    }
    render() {
        return (
            <nav aria-label="breadcrumb">
                <ol className="breadcrumb">
                    {/*<li className="breadcrumb-item"><a href="#">Home</a></li>*/}
                    {/*<li className="breadcrumb-item active" aria-current="page">Library</li>*/}
                    {this.props.list.map((Bread,index)=>{
                        return(
                            <li key={index} className={this.generateClass(index)}><Link to={Bread[1]}>{Bread[0]}</Link></li>
                        )
                    })}
                </ol>
            </nav>
        );
    }
}

export default Breadcumb;