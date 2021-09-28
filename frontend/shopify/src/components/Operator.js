import React, {Component} from 'react';

class Operator extends Component {
    handleIncrement = () =>{
        const { id, orders } = this.props
        const orders_copy = orders
        let card = localStorage.getItem('card')
        card = JSON.parse(card)
        orders_copy[id].quantity = orders_copy[id].quantity + 1
        card["orders"] = orders_copy
        localStorage.setItem('card',JSON.stringify(card))
        this.props.updateOrder(orders_copy)
    }
    handleDecrement = () =>{
        const { id, orders } = this.props
        const orders_copy = orders
        let card = localStorage.getItem('card')
        card = JSON.parse(card)
        if (orders_copy[id].quantity === 1){
            return null
        }
        orders_copy[id].quantity = orders_copy[id].quantity - 1
        card["orders"] = orders_copy
        localStorage.setItem('card',JSON.stringify(card))
        this.props.updateOrder(orders_copy)
    }

    handleDelete = () =>{
        const { id, orders } = this.props
        const orders_copy = orders
        let card = localStorage.getItem('card')
        card = JSON.parse(card)
        const removed = card.orders.splice(id,id)
        if (removed.length === 0) {
            localStorage.removeItem('card')
            this.props.updateOrder("")
        }else{
            card["orders"] = card.orders
           localStorage.setItem('card',JSON.stringify(card))
        this.props.updateOrder(card.orders)
        }

    }
    render() {
        return (
            <div>
                <button className='btn btn-primary m-1' onClick={this.handleIncrement}>+</button>
                <button className='btn btn-primary m-1' onClick={this.handleDecrement}>-</button>
                <button className='btn btn-danger m-1' onClick={this.handleDelete}>delete</button>
            </div>
        );
    }
}

export default Operator;