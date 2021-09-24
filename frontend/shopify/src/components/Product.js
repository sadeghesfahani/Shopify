import React, {Component} from 'react';
import {Link} from "react-router-dom";

class Product extends Component {

    render() {
        const {image, name, price, product_id} = this.props

        return (
            <div className='col-xs-12 col-sm-6 col-md-3 col-lg-3 p-0'>
                <Link to={`/product/${product_id}`}>
                <div className='card'>
                    <img className="card-img-top p-3" src={image} alt="Card image cap"/>
                    <div className='card-body'>
                        <h5 className="card-title">{name}</h5>
                        <p className="card-text">{price} تومان </p>
                    </div>
                </div>
                    </Link>
            </div>

        );
    }
}

export default Product;