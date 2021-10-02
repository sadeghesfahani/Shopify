import React, {Component} from 'react';
import Operator from "./Operator";
import {Link, withRouter, Redirect} from "react-router-dom";
import User from "./User";

class Checkout extends Component {
    state = {
        discount: "",
        discountValidation: "",
        discountPercent: 0
    }

    totalPrice = () => {
        if (this.props.orders) {
            var price = 0
            for (let order of this.props.orders) {
                console.log(order)
                price = price + order.price * order.quantity
            }
            return price
        }
    }
    totalPriceWithDiscount = () => {
        const totalPrice = this.totalPrice()
        const withDiscount = totalPrice * (100 - this.state.discountPercent) / 100
        return withDiscount
    }
    generateList = () => {
        return (


            <table className="table">
                <thead>
                <tr>

                    <th scope="col">نام محصول</th>
                    <th scope="col">تعداد</th>
                    <th scope="col">قیمت واحد</th>
                    <th scope="col">قیمت کل</th>
                    <th scope="col"/>
                </tr>
                </thead>
                <tbody>
                {this.props.orders && this.props.orders.map((order, index) => {
                    return (
                        <tr key={index}>
                            <td>{order.name}</td>
                            <td>{order.quantity}</td>
                            <td>{order.price}</td>
                            <td>{order.price * order.quantity}</td>
                            <td><Operator id={index} orders={this.props.orders} updateOrder={this.props.updateOrder}/>
                            </td>

                            {/*<li key={index} className="list-group-item">{order.name} {order.quantity}<Operator/></li>*/}
                        </tr>
                    )
                })}
                <tr>
                    <td>جمع کل:</td>
                    <td>{this.state.discountValidation && this.totalPriceWithDiscount() || this.totalPrice()}</td>
                    <td></td>
                    <td></td>
                    <td></td>
                </tr>

                </tbody>
            </table>

        )
    }
    handleChange = ({currentTarget: input}) => {
        this.setState({discount: input.value})
    }
    checkDiscount = () => {
        const option = {
            method: "GET",
            headers: {
                'Accept': 'application/json, text/plain',
                'Content-Type': 'application/json;charset=UTF-8',
                'Authorization': `token ${this.props.user ? this.props.user : localStorage.getItem('user')}`
            }
        }
        console.log(option)
        const url = `http://127.0.0.1:8000/card/card/discount_validation/?code=${this.state.discount}`
        fetch(url, option).then(response => response.json()).then(data => this.handleValidation(data))
    }
    handleValidation = (data) => {
        if (data.status) {
            this.setState({discountValidation: data.status, discountPercent: data.percent})
            let card = localStorage.getItem('card')
            card = JSON.parse(card)
            card['discount'] = this.state.discount
            localStorage.setItem('card', JSON.stringify(card))

        } else {
            this.setState({discountValidation: false})
        }
    }

    generateCheckout = () => {
        return (
            <>
                <label htmlFor='discount'>کد تخفیف</label>
                <input type="text" id='discount' name="discount" value={this.state.discount}
                       onChange={this.handleChange}/>
                <button onClick={this.checkDiscount}>ثبت</button>
                {console.log(this.state.discountValidation)}
                {this.state.discountValidation && <h1>yes</h1>}
                {!this.state.discountValidation && <h1>No</h1>}
                {this.generateUser()}
            </>

        )
    }


    generateLog = () => {
        this.props.redirectTo('/checkout')
        return (
            <>
                <Link to='/login'> ورود </Link>
                <Link to="/register"> ثبت نام </Link>
            </>
        )
    }

    generateUser =()=>{
                    return <User/>

    }
    information = () =>{
        if (this.props.loggedIn){

            return this.generateCheckout()

        } else {
            return this.generateLog()
        }
    }

    render() {
        return (
            <div>
                {this.generateList()}
                {this.information()}
                {/*{this.props.loggedIn && this.generateCheckout() || this.generateLog()}*/}


            </div>
        );
    }
    async componentDidMount() {
        let card = localStorage.getItem('card')
        card = JSON.parse(card)
        if(card['discount']){
            await this.setState({discount:card['discount']})
            this.checkDiscount()
        }
    }

}

export default withRouter(Checkout);