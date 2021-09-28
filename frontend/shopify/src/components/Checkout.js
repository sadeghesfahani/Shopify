import React, {Component} from 'react';
import Operator from "./Operator";

class Checkout extends Component {
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
                            <td><Operator id={index} orders={this.props.orders} updateOrder={this.props.updateOrder}/></td>

                            {/*<li key={index} className="list-group-item">{order.name} {order.quantity}<Operator/></li>*/}
                        </tr>
                    )
                })}
                <tr>
                    <td/>
                    <td/>
                    <td/>
                    <td>asd</td>
                    <td/>
                </tr>

                </tbody>
            </table>

        )
    }

    render() {
        return (
            <div>
                {this.generateList()}
            </div>
        );
    }
}

export default Checkout;