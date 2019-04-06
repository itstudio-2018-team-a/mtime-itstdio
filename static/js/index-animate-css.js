let leftEdge = $(document.getElementById("left_edge"));
let left_edge_img = $("#left_edge_img");
let rightEdge = $(document.getElementById("right_edge"));
let right_edge_img = $("#right_edge_img");
let middleLeftEdge = $(document.getElementById("middle_left"));
let middle_left_img = $("#middle_left_img");
let middleRightEdge = $(document.getElementById("middle_right"));
let middle_right_img = $("#middle_right_img");
let movieContainer = $("#movie_container");
/***
 * 事件锁
 * @type {number}
 */
let lock = 0;
const DEFAULT_VALUE = {
    "width": "378px",
    "height": "227px",
    "animate_width": "466px",
    "animate_height": "282px",
    "middle_left": {
        "margin-left": "-78px",
        "margin-right": "-39px",
    },
    "middle_right": {
        "margin-left": "-39px",
        "margin-right": "-78px",
    },
    // "margin_top": ((Number(this.height - "px") - Number(this.animate_height - "px"))) + "px",
    // "margin_left": (Number((this.width - "px") - Number(this.animate_width - "px"))) + "px",
    // "margin_right": (Number((this.width - "px") - Number(this.animate_width - "px"))) + "px"
};
/***
 * 左侧动画
 */
let leftEdgeEnterHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        left_edge_img.animate({
            "width": DEFAULT_VALUE.animate_width,
            "height": DEFAULT_VALUE.animate_height
        });
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": "-126px",
            "marginRight": "-64px"
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": "-39px",
            "marginRight": "-101px"
        })
    })});
};
let leftEdgeOutHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        left_edge_img.animate({
            "width": DEFAULT_VALUE.width,
            "height": DEFAULT_VALUE.height
        });
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_left["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_left["margin-right"]
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_right["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_right["margin-right"]
        })
    })});
};

/**
 * 右侧动画
 * */
let rightEdgeMoveHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        right_edge_img.animate({
            "width": DEFAULT_VALUE.animate_width,
            "height": DEFAULT_VALUE.animate_height
        })
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": "-126px",
            "marginRight": "-64px"
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": "-39px",
            "marginRight": "-101px"
        })
    })});
};
let rightEdgeOutHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        right_edge_img.animate({
            "width": DEFAULT_VALUE.width,
            "height": DEFAULT_VALUE.height
        })
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_left["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_left["margin-right"]
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_right["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_right["margin-right"]
        })
    }, 1)});
};
/***
 * 中左动画
 */
let middleLeftMoveHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        middle_left_img.animate({
            "width": DEFAULT_VALUE.animate_width,
            "height": DEFAULT_VALUE.animate_height
        })
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": "-102px",
            "marginRight": "-83px"
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginRight": "-103px"
        })
    }, 1);});
};
let middleLeftOutHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        middle_left_img.animate({
            "width": DEFAULT_VALUE.width,
            "height": DEFAULT_VALUE.height
        })
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_left["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_left["margin-right"]
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_right["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_right["margin-right"]
        })
    }, 1)});
};
/***
 * 中由动画
 */
let middleRightMoveHandler = ()=>{
    new Promise((resolve, reject)=> {
        setTimeout(() => {
            middle_right_img.animate({
                "width": DEFAULT_VALUE.animate_width,
                "height": DEFAULT_VALUE.animate_height
            })
        }, 1);
        setTimeout(() => {
            middleLeftEdge.animate({
                "marginLeft": "-102px",
                "marginRight": "-64px"
            })
        }, 1);
        setTimeout(() => {
            middleRightEdge.animate({
                "marginLeft": "-39px",
                "marginRight": "-123px"
            })
        })
    });
};
let middleRightOutHandler = ()=>{
    new Promise(()=>{setTimeout(()=>{
        middle_right_img.animate({
            "width": DEFAULT_VALUE.width,
            "height": DEFAULT_VALUE.height
        })
    },1);
    setTimeout(()=>{
        middleLeftEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_left["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_left["margin-right"]
        })
    }, 1);
    setTimeout(()=>{
        middleRightEdge.animate({
            "marginLeft": DEFAULT_VALUE.middle_right["margin-left"],
            "marginRight": DEFAULT_VALUE.middle_right["margin-right"]
        })
    }, 1)});
};

/***
 * 获取target
 * @param event
 * @returns {*|Element|Object}
 */
function getTarget(event){
    return event.target || event.srcElement;
}
/***
 * 获取相关事件
 */
function getRelatedTarget(event){
    return event.relatedTarget || event.fromElement;
}
/**
 * 事件代理
 * */
let debounce = (func)=> {
    let timer;
    return ()=>{
        clearTimeout(timer);
        timer = setTimeout(func, 1000);
    }
};
movieContainer.on("mouseover",(event)=>{
    debounce(()=>{
        let target = getTarget(event);
        let relatedTarget = getRelatedTarget(event);
        for(let element = relatedTarget; element; element = element.parentNode){
            if(element === target && element.id && (element.id === "left_edge" || element.id === "right_edge" || element.id === "middle_left" || element.id === "middle_right")) {
                return;
            }
        }
        let types = {
            "left_edge_img": leftEdgeEnterHandler,
            "right_edge_img": rightEdgeMoveHandler,
            "middle_left_img": middleLeftMoveHandler,
            "middle_right_img": middleRightMoveHandler
        };
        if(lock === 0) {
            if (types[target.id]) {
                types[target.id]();
                lock = 1;
            }
        }else{
            return null;
        }
    })();
});
movieContainer.on("mouseout",(event)=>{
    let target = getTarget(event);
    let relatedTarget = getRelatedTarget(event);
    for(let element = relatedTarget; element; element = element.parentNode){
        if(element === target && element.id && (element.id === "left_edge" || element.id === "right_edge" || element.id === "middle_left" || element.id === "middle_right")) {
            return;
        }
    }
    let types = {
        "left_edge_img": leftEdgeOutHandler,
        "right_edge_img": rightEdgeOutHandler,
        "middle_left_img": middleLeftOutHandler,
        "middle_right_img": middleRightOutHandler
    };
    if(lock === 1) {
        if (types[target.id]) {
            types[target.id]();
            lock = 0;
        }
    }
});

