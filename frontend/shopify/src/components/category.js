import React, {Component} from 'react';
import Breadcumb from "./Breadcumb";

class Category extends Component {

    generateBreadcumb(allInstances, activeInstance_id, property, baseUrl) {
        let activeInstance = this.getInstance(allInstances, activeInstance_id)
        const listToPass = []

        do {
            let microList = [activeInstance.name, baseUrl + activeInstance.id]
            if (activeInstance[property] != null) {
                activeInstance = this.getInstance(allInstances, activeInstance[property]['id'])
            }
            listToPass.push(microList)
        } while (activeInstance[property] === undefined)

        let microList = [activeInstance.name, baseUrl + activeInstance.id]

        if (microList[1] !== listToPass[0][1]) {
            listToPass.push(microList)
        }

        return listToPass.reverse()
    }

    getInstance(allInstances, instanceId) {
        for (let instance of allInstances) {
            if (String(instance.id) === String(instanceId)) return instance
        }
    }

    render() {
        return (
            <div>
                {this.props.category.length !== 0 && <Breadcumb
                    list={this.generateBreadcumb(this.props.category, this.props.match.params.id, 'parent', '/category/')}/>}
            </div>
        );
    }
}

export default Category;