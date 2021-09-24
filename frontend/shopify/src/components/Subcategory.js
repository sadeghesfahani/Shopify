import React, {Component} from 'react';
import {Link} from "react-router-dom";

class Subcategory extends Component {
    render() {
        return (
            <div className='col-12 p-0 '>
                <ul className="list-group p-0 m-0">
                    {this.props.subcategories.map((category,index)=>{
                        return(
                            <Link key={index} to={`/category/${category.id}`} className='list-group-item list-group-item-action' >{category.name}</Link>
                        )
                    })}
                </ul>
            </div>
        );
    }
}

export default Subcategory;