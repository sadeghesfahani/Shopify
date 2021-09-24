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
                    {this.props.parents.map((category,index)=>{
                        return(
                            <li key={index} className='breadcrumb-item'><Link to={`/category/${category.id}`}>{category.name}</Link></li>
                        )
                    })}
                </ol>
            </nav>
        );
    }
}

export default Breadcumb;